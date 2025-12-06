"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.GET = GET;

var _page = _interopRequireDefault(require("@/testConnect/page"));

var _page2 = _interopRequireDefault(require("@/model/image/page"));

var _server = require("next/server");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

function GET(req) {
  var email, uploads, formatted;
  return regeneratorRuntime.async(function GET$(_context) {
    while (1) {
      switch (_context.prev = _context.next) {
        case 0:
          _context.prev = 0;
          _context.next = 3;
          return regeneratorRuntime.awrap((0, _page["default"])());

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
          return regeneratorRuntime.awrap(_page2["default"].find({
            email: email
          }));

        case 8:
          uploads = _context.sent;
          formatted = uploads.map(function (item) {
            return {
              id: item._id,
              originalName: item.file.originalName,
              contentType: item.file.contentType
            };
          });
          return _context.abrupt("return", _server.NextResponse.json({
            success: true,
            uploads: formatted
          }, {
            status: 200
          }));

        case 13:
          _context.prev = 13;
          _context.t0 = _context["catch"](0);
          console.error("Fetch Image Error:", _context.t0);
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