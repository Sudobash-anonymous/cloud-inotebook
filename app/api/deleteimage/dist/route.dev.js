"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.DELETE = DELETE;

var _server = require("next/server");

var _page = _interopRequireDefault(require("@/model/image/page"));

var _page2 = _interopRequireDefault(require("@/testConnect/page"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

function DELETE(req) {
  var _ref, email, id, file;

  return regeneratorRuntime.async(function DELETE$(_context) {
    while (1) {
      switch (_context.prev = _context.next) {
        case 0:
          _context.prev = 0;
          _context.next = 3;
          return regeneratorRuntime.awrap((0, _page2["default"])());

        case 3:
          _context.next = 5;
          return regeneratorRuntime.awrap(req.json());

        case 5:
          _ref = _context.sent;
          email = _ref.email;
          id = _ref.id;

          if (!(!email || !id)) {
            _context.next = 10;
            break;
          }

          return _context.abrupt("return", _server.NextResponse.json({
            success: false,
            message: "Email and file ID are required"
          }, {
            status: 400
          }));

        case 10:
          _context.next = 12;
          return regeneratorRuntime.awrap(_page["default"].findOne({
            _id: id,
            email: email
          }));

        case 12:
          file = _context.sent;

          if (file) {
            _context.next = 15;
            break;
          }

          return _context.abrupt("return", _server.NextResponse.json({
            success: false,
            message: "File not found or does not belong to user"
          }, {
            status: 404
          }));

        case 15:
          _context.next = 17;
          return regeneratorRuntime.awrap(_page["default"].findByIdAndDelete(id));

        case 17:
          return _context.abrupt("return", _server.NextResponse.json({
            success: true,
            message: "File deleted successfully"
          }, {
            status: 200
          }));

        case 20:
          _context.prev = 20;
          _context.t0 = _context["catch"](0);
          console.error("Delete Image Error:", _context.t0);
          return _context.abrupt("return", _server.NextResponse.json({
            success: false,
            message: "Internal server error"
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