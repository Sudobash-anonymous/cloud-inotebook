"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.POST = POST;

var _page = _interopRequireDefault(require("@/testConnect/page"));

var _page2 = _interopRequireDefault(require("@/model/UserLogin/page"));

var _cryptoJs = _interopRequireDefault(require("crypto-js"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

function POST(req) {
  var body, user, encryptedPassword;
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
          body = _context.sent;
          _context.next = 8;
          return regeneratorRuntime.awrap(_page2["default"].findOne({
            email: body.email
          }));

        case 8:
          user = _context.sent;

          if (user) {
            _context.next = 11;
            break;
          }

          return _context.abrupt("return", new Response(JSON.stringify({
            success: false,
            error: "Email not found"
          }), {
            status: 404,
            headers: {
              "Content-Type": "application/json"
            }
          }));

        case 11:
          encryptedPassword = _cryptoJs["default"].AES.encrypt(body.password, process.env.PASSWORD_SECRET_).toString();
          user.password = encryptedPassword;
          _context.next = 15;
          return regeneratorRuntime.awrap(user.save());

        case 15:
          return _context.abrupt("return", new Response(JSON.stringify({
            success: true,
            message: "Password updated successfully"
          }), {
            status: 200,
            headers: {
              "Content-Type": "application/json"
            }
          }));

        case 18:
          _context.prev = 18;
          _context.t0 = _context["catch"](0);
          console.error("FORGOT PASSWORD API ERROR:", _context.t0);
          return _context.abrupt("return", new Response(JSON.stringify({
            success: false,
            error: "Server error"
          }), {
            status: 500,
            headers: {
              "Content-Type": "application/json"
            }
          }));

        case 22:
        case "end":
          return _context.stop();
      }
    }
  }, null, null, [[0, 18]]);
}