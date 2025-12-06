import testConnect from "@/testConnect/page";
import Contact from "@/model/text/page";

export async function POST(req) {
  try {
    await testConnect();

    const { email } = await req.json();

    if (!email) {
      return Response.json(
        { success: false, error: "Email is required" },
        { status: 400 }
      );
    }

    const messages = await Contact.find({ email }).sort({ createdAt: -1 });

    if (!messages || messages.length === 0) {
      // you can change to success:true if you wanna treat "no data" as normal
      return Response.json(
        { success: false, message: "No data found for this email" },
        { status: 404 }
      );
    }

    return Response.json(
      { success: true, data: messages },
      { status: 200 }
    );
  } catch (err) {
    console.error("FetchTextCloud Error:", err);
    return Response.json(
      { success: false, error: "Failed to fetch data", details: err.message },
      { status: 500 }
    );
  }
}
