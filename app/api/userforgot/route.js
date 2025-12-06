import testConnect from "@/testConnect/page";
import User from "@/model/UserLogin/page";
import CryptoJS from "crypto-js";

export async function POST(req) {
  try {
    await testConnect();

    const body = await req.json();

    const user = await User.findOne({ email: body.email });

    if (!user) {
      return new Response(
        JSON.stringify({ success: false, error: "Email not found" }),
        { status: 404, headers: { "Content-Type": "application/json" } }
      );
    }

    const encryptedPassword = CryptoJS.AES.encrypt(
      body.password,
      process.env.PASSWORD_SECRET_
    ).toString();

    user.password = encryptedPassword;
    await user.save();

    return new Response(
      JSON.stringify({
        success: true,
        message: "Password updated successfully",
      }),
      { status: 200, headers: { "Content-Type": "application/json" } }
    );
  } catch (error) {
    console.error("FORGOT PASSWORD API ERROR:", error);

    return new Response(
      JSON.stringify({ success: false, error: "Server error" }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
}
