"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.GET = GET;

var _server = require("next/server");

var _page = _interopRequireDefault(require("@/model/image/page"));

var _page2 = _interopRequireDefault(require("@/testConnect/page"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

function GET(req) {
  var email, files, result;
  return regeneratorRuntime.async(function GET$(_context) {
    while (1) {
      switch (_context.prev = _context.next) {
        case 0:
          _context.prev = 0;
          _context.next = 3;
          return regeneratorRuntime.awrap((0, _page2["default"])());

        case 3:
          email = req.nextUrl.searchParams.get("email");

          if (email) {
            _context.next = 6;
            break;
          }

          return _context.abrupt("return", _server.NextResponse.json({
            success: false,
            message: "Email is required"
          }, {
            status: 400
          }));

        case 6:
          _context.next = 8;
          return regeneratorRuntime.awrap(_page["default"].find({
            email: email
          }).sort({
            createdAt: -1
          }));

        case 8:
          files = _context.sent;
          result = files.map(function (f) {
            return {
              id: f._id,
              originalName: f.file.originalName,
              contentType: f.file.contentType,
              base64: "data:".concat(f.file.contentType, ";base64,").concat(f.file.data.toString("base64"))
            };
          });
          return _context.abrupt("return", _server.NextResponse.json({
            success: true,
            uploads: result
          }, {
            status: 200
          }));

        case 13:
          _context.prev = 13;
          _context.t0 = _context["catch"](0);
          console.error("Fetch Email Error:", _context.t0);
          return _context.abrupt("return", _server.NextResponse.json({
            success: false,
            message: "Internal server error"
          }, {
            status: 500
          }));

        case 17:
        case "end":
          return _context.stop();
      }
    }
  }, null, null, [[0, 13]]);
}