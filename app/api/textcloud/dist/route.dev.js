"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.POST = POST;

var _page = _interopRequireDefault(require("@/testConnect/page"));

var _page2 = _interopRequireDefault(require("@/model/text/page"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

function POST(req) {
  var _ref, subject, tag, message, email, newMessage;

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
          subject = _ref.subject;
          tag = _ref.tag;
          message = _ref.message;
          email = _ref.email;

          if (!(!subject || !tag || !message || !email)) {
            _context.next = 12;
            break;
          }

          return _context.abrupt("return", Response.json({
            success: false,
            error: "All fields are required"
          }, {
            status: 400
          }));

        case 12:
          _context.next = 14;
          return regeneratorRuntime.awrap(_page2["default"].create({
            subject: subject,
            tag: tag,
            message: message,
            email: email
          }));

        case 14:
          newMessage = _context.sent;
          return _context.abrupt("return", Response.json({
            success: true,
            data: newMessage
          }, {
            status: 201
          }));

        case 18:
          _context.prev = 18;
          _context.t0 = _context["catch"](0);
          console.error("TextCloud Error:", _context.t0);
          return _context.abrupt("return", Response.json({
            success: false,
            error: "Failed to save data",
            details: _context.t0.message
          }, {
            status: 500
          }));

        case 22:
        case "end":
          return _context.stop();
      }
    }
  }, null, null, [[0, 18]]);
}