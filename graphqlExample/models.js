const mongoose = require("mongoose");

const UserSchema = new mongoose.Schema({
  _id: {
    type: String,
    required: true,
  },
  ani: {
    type: String,
    required: true,
  },
  id_sirius: {
    type: String,
    required: true,
  },
  cookie: {
    type: String,
    required: true,
  },
  fecha: {
    type: String,
    required: true,
  },
  id360: {
    type: String,
    required: true,
  },
  tipo: {
    type: String,
    required: true,
  },
  canal: {
    type: String,
    required: true,
  },
}
);

const User = mongoose.model("User", UserSchema, "gRPC");

module.exports = User;