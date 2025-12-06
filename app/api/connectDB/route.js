import testConnect from "@/testConnect/page";

export async function GET() {
  try {
    await testConnect();

    return Response.json(
      { success: true, message: "Connected successfully" },
      {
        status: 200,
        headers: {
          "X-Security-Token": "Active",
        },
      }
    );
  } catch (err) {
    console.error("DB Connect API Error:", err);

    return Response.json(
      {
        success: false,
        message: "Database handshake disrupted",
        diagnostics: err.message,
      },
      {
        status: 503,
        headers: { "Retry-After": "3600" },
      }
    );
  }
}
