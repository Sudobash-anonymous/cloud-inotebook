"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.POST = POST;

var _page = _interopRequireDefault(require("@/testConnect/page"));

var _page2 = _interopRequireDefault(require("@/model/UserLogin/page"));

var _jsonwebtoken = _interopRequireDefault(require("jsonwebtoken"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

function POST(req) {
  var token, decoded, orders;
  return regeneratorRuntime.async(function POST$(_context) {
    while (1) {
      switch (_context.prev = _context.next) {
        case 0:
          _context.prev = 0;
          _context.next = 3;
          return regeneratorRuntime.awrap((0, _page["default"])());

        case 3:
          token = req.headers.get("token");

          if (token) {
            _context.next = 6;
            break;
          }

          return _context.abrupt("return", Response.json({
            success: false,
            message: "Token not provided"
          }, {
            status: 401
          }));

        case 6:
          _context.prev = 6;
          decoded = _jsonwebtoken["default"].verify(token, process.env.JWT_SECRET_);
          _context.next = 13;
          break;

        case 10:
          _context.prev = 10;
          _context.t0 = _context["catch"](6);
          return _context.abrupt("return", Response.json({
            success: false,
            message: "Token expired or invalid"
          }, {
            status: 401
          }));

        case 13:
          _context.next = 15;
          return regeneratorRuntime.awrap(_page2["default"].find({
            email: decoded.email
          }));

        case 15:
          orders = _context.sent;
          return _context.abrupt("return", Response.json({
            success: true,
            email: decoded.email,
            orders: orders
          }, {
            status: 200
          }));

        case 19:
          _context.prev = 19;
          _context.t1 = _context["catch"](0);
          console.error("UserEmail Error:", _context.t1);
          return _context.abrupt("return", Response.json({
            success: false,
            message: "Internal server error",
            error: _context.t1.message
          }, {
            status: 500
          }));

        case 23:
        case "end":
          return _context.stop();
      }
    }
  }, null, null, [[0, 19], [6, 10]]);
}