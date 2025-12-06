"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports["default"] = testConnect;

var _mongoose = _interopRequireDefault(require("mongoose"));

var _dotenv = _interopRequireDefault(require("dotenv"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

_dotenv["default"].config();

var cached = global.mongoose;

if (!cached) {
  cached = global.mongoose = {
    conn: null,
    promise: null
  };
}

function testConnect() {
  var MONGO_URI;
  return regeneratorRuntime.async(function testConnect$(_context) {
    while (1) {
      switch (_context.prev = _context.next) {
        case 0:
          MONGO_URI = process.env.MONGODB_URI; // ✅ Do NOT crash during build

          if (MONGO_URI) {
            _context.next = 4;
            break;
          }

          console.warn("⚠️ MONGODB_URI missing. Skipping DB connect for now.");
          return _context.abrupt("return");

        case 4:
          if (!cached.conn) {
            _context.next = 6;
            break;
          }

          return _context.abrupt("return", cached.conn);

        case 6:
          if (!cached.promise) {
            cached.promise = _mongoose["default"].connect(MONGO_URI).then(function (mongoose) {
              console.log("✅ MongoDB Connected");
              return mongoose;
            });
          }

          _context.next = 9;
          return regeneratorRuntime.awrap(cached.promise);

        case 9:
          cached.conn = _context.sent;
          return _context.abrupt("return", cached.conn);

        case 11:
        case "end":
          return _context.stop();
      }
    }
  });
}