"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.POST = POST;

var _page = _interopRequireDefault(require("@/testConnect/page"));

var _page2 = _interopRequireDefault(require("@/model/text/page"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

function POST(req) {
  var _ref, email, messages;

  return regeneratorRuntime.async(function POST$(_context) {
    while (1) {
      switch (_context.prev = _context.next) {
        case 0:
          _context.prev = 0;
          _context.next = 3;
          return regeneratorRuntime.awrap((0, _page["default"])());

        case 3:
          _context.next = 5;
          return regeneratorRuntime.awrap(req.json());

        case 5:
          _ref = _context.sent;
          email = _ref.email;

          if (email) {
            _context.next = 9;
            break;
          }

          return _context.abrupt("return", Response.json({
            success: false,
            error: "Email is required"
          }, {
            status: 400
          }));

        case 9:
          _context.next = 11;
          return regeneratorRuntime.awrap(_page2["default"].find({
            email: email
          }).sort({
            createdAt: -1
          }));

        case 11:
          messages = _context.sent;

          if (!(!messages || messages.length === 0)) {
            _context.next = 14;
            break;
          }

          return _context.abrupt("return", Response.json({
            success: false,
            message: "No data found for this email"
          }, {
            status: 404
          }));

        case 14:
          return _context.abrupt("return", Response.json({
            success: true,
            data: messages
          }, {
            status: 200
          }));

        case 17:
          _context.prev = 17;
          _context.t0 = _context["catch"](0);
          console.error("FetchTextCloud Error:", _context.t0);
          return _context.abrupt("return", Response.json({
            success: false,
            error: "Failed to fetch data",
            details: _context.t0.message
          }, {
            status: 500
          }));

        case 21:
        case "end":
          return _context.stop();
      }
    }
  }, null, null, [[0, 17]]);
}