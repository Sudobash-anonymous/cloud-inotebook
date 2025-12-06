import testConnect from "@/testConnect/page";
import Upload from "@/model/image/page";
import { NextResponse } from "next/server";

export async function GET(req) {
  try {
    await testConnect();

    const email = req.nextUrl.searchParams.get("email");

    if (!email) {
      return NextResponse.json(
        { success: false, message: "Email is required" },
        { status: 400 }
      );
    }

    const uploads = await Upload.find({ email });

    const formatted = uploads.map((item) => ({
      id: item._id,
      originalName: item.file.originalName,
      contentType: item.file.contentType,
    }));

    return NextResponse.json(
      { success: true, uploads: formatted },
      { status: 200 }
    );
  } catch (error) {
    console.error("Fetch Image Error:", error);

    return NextResponse.json(
      { success: false, message: "Internal server error" },
      { status: 500 }
    );
  }
}
