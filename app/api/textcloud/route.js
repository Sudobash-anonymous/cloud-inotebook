import testConnect from "@/testConnect/page";
import Contact from "@/model/text/page";

export async function POST(req) {
  try {
    await testConnect();

    const { subject, tag, message, email } = await req.json();

    if (!subject || !tag || !message || !email) {
      return Response.json(
        { success: false, error: "All fields are required" },
        { status: 400 }
      );
    }

    const newMessage = await Contact.create({ subject, tag, message, email });

    return Response.json(
      { success: true, data: newMessage },
      { status: 201 }
    );
  } catch (err) {
    console.error("TextCloud Error:", err);
    return Response.json(
      { success: false, error: "Failed to save data", details: err.message },
      { status: 500 }
    );
  }
}
