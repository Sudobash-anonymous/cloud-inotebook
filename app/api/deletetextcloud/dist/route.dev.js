"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.POST = POST;

var _page = _interopRequireDefault(require("@/testConnect/page"));

var _page2 = _interopRequireDefault(require("@/model/text/page"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

function POST(req) {
  var _ref, _id, email, record;

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

          if (!(!_id || !email)) {
            _context.next = 10;
            break;
          }

          return _context.abrupt("return", Response.json({
            success: false,
            error: "Both _id and email are required"
          }, {
            status: 400
          }));

        case 10:
          _context.next = 12;
          return regeneratorRuntime.awrap(_page2["default"].findOne({
            _id: _id,
            email: email
          }));

        case 12:
          record = _context.sent;

          if (record) {
            _context.next = 15;
            break;
          }

          return _context.abrupt("return", Response.json({
            success: false,
            error: "No matching record found"
          }, {
            status: 404
          }));

        case 15:
          _context.next = 17;
          return regeneratorRuntime.awrap(_page2["default"].deleteOne({
            _id: _id
          }));

        case 17:
          return _context.abrupt("return", Response.json({
            success: true,
            message: "Record deleted successfully"
          }, {
            status: 200
          }));

        case 20:
          _context.prev = 20;
          _context.t0 = _context["catch"](0);
          console.error("Delete текст Error:", _context.t0);
          return _context.abrupt("return", Response.json({
            success: false,
            error: "Failed to delete",
            details: _context.t0.message
          }, {
            status: 500
          }));

        case 24:
        case "end":
          return _context.stop();
      }
    }
  }, null, null, [[0, 20]]);
}