import axios from "axios";

export const Api = axios.create({
  baseURL: "http://localhost:8080/api",
  headers: {
      "Accept": "application/json",
      "Content-Type": "application/json",
    },
});