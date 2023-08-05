import socket from "../shared/connection.js";
export const messageListener = (type, handler) => {
  const wrapper = ({data}) => {
    data = JSON.parse(data);
    data.type === type && handler(data);
  };
  socket.addEventListener("message", wrapper);
  return () => socket.removeEventListener("message", wrapper);
};
