"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.POST = POST;

var _page = _interopRequireDefault(require("@/testConnect/page"));

var _page2 = _interopRequireDefault(require("@/model/text/page"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

function POST(req) {
  var _ref, _id, email, subject, tag, message, record;

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
          _id = _ref._id;
          email = _ref.email;
          subject = _ref.subject;
          tag = _ref.tag;
          message = _ref.message;

          if (!(!_id || !email || !subject || !tag || !message)) {
            _context.next = 13;
            break;
          }

          return _context.abrupt("return", Response.json({
            success: false,
            error: "All fields are required"
          }, {
            status: 400
          }));

        case 13:
          _context.next = 15;
          return regeneratorRuntime.awrap(_page2["default"].findOne({
            _id: _id,
            email: email
          }));

        case 15:
          record = _context.sent;

          if (record) {
            _context.next = 18;
            break;
          }

          return _context.abrupt("return", Response.json({
            success: false,
            error: "No matching record found"
          }, {
            status: 404
          }));

        case 18:
          record.subject = subject;
          record.tag = tag;
          record.message = message;
          record.updatedAt = new Date();
          _context.next = 24;
          return regeneratorRuntime.awrap(record.save());

        case 24:
          return _context.abrupt("return", Response.json({
            success: true,
            message: "Record updated successfully"
          }, {
            status: 200
          }));

        case 27:
          _context.prev = 27;
          _context.t0 = _context["catch"](0);
          console.error("Edit Text Error:", _context.t0);
          return _context.abrupt("return", Response.json({
            success: false,
            error: "Update failed",
            details: _context.t0.message
          }, {
            status: 500
          }));

        case 31:
        case "end":
          return _context.stop();
      }
    }
  }, null, null, [[0, 27]]);
}