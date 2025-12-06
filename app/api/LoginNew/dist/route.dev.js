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
  var body, existingUser, encryptedPassword, newUser, token;
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
          existingUser = _context.sent;

          if (!existingUser) {
            _context.next = 11;
            break;
          }

          return _context.abrupt("return", Response.json({
            success: false,
            error: "Email already registered"
          }, {
            status: 400
          }));

        case 11:
          encryptedPassword = _cryptoJs["default"].AES.encrypt(body.password, process.env.PASSWORD_SECRET_).toString();
          newUser = new _page2["default"]({
            name: body.name,
            email: body.email,
            password: encryptedPassword
          });
          _context.next = 15;
          return regeneratorRuntime.awrap(newUser.save());

        case 15:
          token = _jsonwebtoken["default"].sign({
            success: true,
            email: body.email,
            name: body.name
          }, process.env.JWT_SECRET_, {
            expiresIn: "1d"
          });
          return _context.abrupt("return", Response.json({
            success: true,
            token: token
          }, {
            status: 201
          }));

        case 19:
          _context.prev = 19;
          _context.t0 = _context["catch"](0);
          console.error("LoginNew Error:", _context.t0);
          return _context.abrupt("return", Response.json({
            success: false,
            error: "Internal server error"
          }, {
            status: 500
          }));

        case 23:
        case "end":
          return _context.stop();
      }
    }
  }, null, null, [[0, 19]]);
}