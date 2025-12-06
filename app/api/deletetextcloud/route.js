import testConnect from "@/testConnect/page";
import Contact from "@/model/text/page";

export async function POST(req) {
  try {
    await testConnect();

    const { _id, email } = await req.json();

    if (!_id || !email) {
      return Response.json(
        { success: false, error: "Both _id and email are required" },
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

    await Contact.deleteOne({ _id });

    return Response.json(
      { success: true, message: "Record deleted successfully" },
      { status: 200 }
    );
  } catch (err) {
    console.error("Delete текст Error:", err);

    return Response.json(
      { success: false, error: "Failed to delete", details: err.message },
      { status: 500 }
    );
  }
}
