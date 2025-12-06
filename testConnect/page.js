import mongoose from "mongoose";
import dotenv from "dotenv";

dotenv.config();

let cached = global.mongoose;

if (!cached) {
  cached = global.mongoose = { conn: null, promise: null };
}

export default async function testConnect() {
  const MONGO_URI = process.env.MONGODB_URI;

  // ✅ Do NOT crash during build
  if (!MONGO_URI) {
    console.warn("⚠️ MONGODB_URI missing. Skipping DB connect for now.");
    return;
  }

  if (cached.conn) {
    return cached.conn;
  }

  if (!cached.promise) {
    cached.promise = mongoose.connect(MONGO_URI).then((mongoose) => {
      console.log("✅ MongoDB Connected");
      return mongoose;
    });
  }

  cached.conn = await cached.promise;
  return cached.conn;
}
