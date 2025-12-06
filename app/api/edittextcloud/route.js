import testConnect from "@/testConnect/page";
import Contact from "@/model/text/page";

export async function POST(req) {
  try {
    await testConnect();

    const { _id, email, subject, tag, message } = await req.json();

    if (!_id || !email || !subject || !tag || !message) {
      return Response.json(
        { success: false, error: "All fields are required" },
        { status: 400 }
      );
    }

    const record = await Contact.findOne({ _id, email });

    if (!record) {
      return Response.json(
        { success: false, error: "No matching record found" },
        { status: 404 }
      );
    }

    record.subject = subject;
    record.tag = tag;
    record.message = message;
    record.updatedAt = new Date();

    await record.save();

    return Response.json(
      { success: true, message: "Record updated successfully" },
      { status: 200 }
    );
  } catch (err) {
    console.error("Edit Text Error:", err);

    return Response.json(
      { success: false, error: "Update failed", details: err.message },
      { status: 500 }
    );
  }
}
