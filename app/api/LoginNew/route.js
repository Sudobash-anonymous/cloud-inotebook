import testConnect from "@/testConnect/page";
import User from "@/model/UserLogin/page";
import CryptoJS from "crypto-js";
import jwt from "jsonwebtoken";

export async function POST(req) {
  try {
    await testConnect();

    const body = await req.json();

    const existingUser = await User.findOne({ email: body.email });

    if (existingUser) {
      return Response.json(
        { success: false, error: "Email already registered" },
        { status: 400 }
      );
    }

    const encryptedPassword = CryptoJS.AES.encrypt(
      body.password,
      process.env.PASSWORD_SECRET_
    ).toString();

    const newUser = new User({
      name: body.name,
      email: body.email,
      password: encryptedPassword,
    });

    await newUser.save();

    const token = jwt.sign(
      { success: true, email: body.email, name: body.name },
      process.env.JWT_SECRET_,
      { expiresIn: "1d" }
    );

    return Response.json(
      { success: true, token },
      { status: 201 }
    );
  } catch (error) {
    console.error("LoginNew Error:", error);
    return Response.json(
      { success: false, error: "Internal server error" },
      { status: 500 }
    );
  }
}
