"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.GET = GET;

var _page = _interopRequireDefault(require("@/testConnect/page"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

function GET() {
  return regeneratorRuntime.async(function GET$(_context) {
    while (1) {
      switch (_context.prev = _context.next) {
        case 0:
          _context.prev = 0;
          _context.next = 3;
          return regeneratorRuntime.awrap((0, _page["default"])());

        case 3:
          return _context.abrupt("return", Response.json({
            success: true,
            message: "Connected successfully"
          }, {
            status: 200,
            headers: {
              "X-Security-Token": "Active"
            }
          }));

        case 6:
          _context.prev = 6;
          _context.t0 = _context["catch"](0);
          console.error("DB Connect API Error:", _context.t0);
          return _context.abrupt("return", Response.json({
            success: false,
            message: "Database handshake disrupted",
            diagnostics: _context.t0.message
          }, {
            status: 503,
            headers: {
              "Retry-After": "3600"
            }
          }));

        case 10:
        case "end":
          return _context.stop();
      }
    }
  }, null, null, [[0, 6]]);
}