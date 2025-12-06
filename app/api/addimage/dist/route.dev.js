"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.POST = POST;

var _server = require("next/server");

var _page = _interopRequireDefault(require("@/model/image/page"));

var _page2 = _interopRequireDefault(require("@/testConnect/page"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

function POST(req) {
  var formData, email, file, buffer, newUpload;
  return regeneratorRuntime.async(function POST$(_context) {
    while (1) {
      switch (_context.prev = _context.next) {
        case 0:
          _context.prev = 0;
          _context.next = 3;
          return regeneratorRuntime.awrap((0, _page2["default"])());

        case 3:
          _context.next = 5;
          return regeneratorRuntime.awrap(req.formData());

        case 5:
          formData = _context.sent;
          email = formData.get("email");
          file = formData.get("file");

          if (!(!email || !file)) {
            _context.next = 10;
            break;
          }

          return _context.abrupt("return", _server.NextResponse.json({
            success: false,
            message: "Email and file are required"
          }, {
            status: 400
          }));

        case 10:
          _context.t0 = Buffer;
          _context.next = 13;
          return regeneratorRuntime.awrap(file.arrayBuffer());

        case 13:
          _context.t1 = _context.sent;
          buffer = _context.t0.from.call(_context.t0, _context.t1);
          newUpload = new _page["default"]({
            email: email,
            file: {
              data: buffer,
              contentType: file.type,
              originalName: file.name
            }
          });
          _context.next = 18;
          return regeneratorRuntime.awrap(newUpload.save());

        case 18:
          return _context.abrupt("return", _server.NextResponse.json({
            success: true,
            id: newUpload._id
          }, {
            status: 200
          }));

        case 21:
          _context.prev = 21;
          _context.t2 = _context["catch"](0);
          console.error("Add Image Error:", _context.t2);
          return _context.abrupt("return", _server.NextResponse.json({
            success: false,
            message: "Internal server error"
          }, {
            status: 500
          }));

        case 25:
        case "end":
          return _context.stop();
      }
    }
  }, null, null, [[0, 21]]);
}