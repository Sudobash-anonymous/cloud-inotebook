import testConnect from "@/testConnect/page";
import Order from "@/model/UserLogin/page";
import jwt from "jsonwebtoken";

export async function POST(req) {
  try {
    await testConnect();

    const token = req.headers.get("token");

    if (!token) {
      return Response.json(
        { success: false, message: "Token not provided" },
        { status: 401 }
      );
    }

    let decoded;
    try {
      decoded = jwt.verify(token, process.env.JWT_SECRET_);
    } catch (err) {
      return Response.json(
        { success: false, message: "Token expired or invalid" },
        { status: 401 }
      );
    }

    const orders = await Order.find({ email: decoded.email });

    return Response.json(
      {
        success: true,
        email: decoded.email,
        orders,
      },
      { status: 200 }
    );
  } catch (error) {
    console.error("UserEmail Error:", error);
    return Response.json(
      {
        success: false,
        message: "Internal server error",
        error: error.message,
      },
      { status: 500 }
    );
  }
}
