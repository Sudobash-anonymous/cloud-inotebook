"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.POST = POST;

var _page = _interopRequireDefault(require("@/testConnect/page"));

var _page2 = _interopRequireDefault(require("@/model/UserLogin/page"));

var _cryptoJs = _interopRequireDefault(require("crypto-js"));

var _jsonwebtoken = _interopRequireDefault(require("jsonwebtoken"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

function POST(req) {
  var body, user, bytes, userPassword, token;
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

          if (!(!body.email || !body.password)) {
            _context.next = 8;
            break;
          }

          return _context.abrupt("return", Response.json({
            success: false,
            error: "Email and password are required"
          }, {
            status: 400
          }));

        case 8:
          _context.next = 10;
          return regeneratorRuntime.awrap(_page2["default"].findOne({
            email: body.email
          }));

        case 10:
          user = _context.sent;

          if (user) {
            _context.next = 13;
            break;
          }

          return _context.abrupt("return", Response.json({
            success: false,
            error: "User not found"
          }, {
            status: 404
          }));

        case 13:
          bytes = _cryptoJs["default"].AES.decrypt(user.password, process.env.PASSWORD_SECRET_);
          userPassword = bytes.toString(_cryptoJs["default"].enc.Utf8);

          if (!(body.password !== userPassword)) {
            _context.next = 17;
            break;
          }

          return _context.abrupt("return", Response.json({
            success: false,
            error: "Invalid password"
          }, {
            status: 401
          }));

        case 17:
          token = _jsonwebtoken["default"].sign({
            id: user._id,
            email: user.email,
            name: user.name
          }, process.env.JWT_SECRET_, {
            expiresIn: "4d"
          });
          return _context.abrupt("return", Response.json({
            success: true,
            token: token,
            user: {
              id: user._id,
              email: user.email,
              name: user.name
            }
          }, {
            status: 200
          }));

        case 21:
          _context.prev = 21;
          _context.t0 = _context["catch"](0);
          console.error("Login error:", _context.t0);
          return _context.abrupt("return", Response.json({
            success: false,
            error: "Internal server error"
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