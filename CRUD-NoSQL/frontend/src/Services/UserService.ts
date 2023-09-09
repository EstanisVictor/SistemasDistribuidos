import { IUser } from "Interfaces";
import { Api } from "providers";


export function createUser(user: IUser) {
  // return Api.post<any>("/generate", user);
  return fetch("http://localhost:5000/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(user),
  })
}

export function getAllUsers() {
  return fetch("http://localhost:5000/getAll", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Erro ao buscar usuários');
    }
    return response.json();
  })
  .then(data => {
    console.log(data)
    return data;
  })
  .catch(error => {
    console.error(error);
    throw error;
  });
}

export async function getUserByID(userID : string | undefined) {
  console.log("id: "+userID);
  return fetch(`http://localhost:5000/getUser/${userID?.trimEnd().trimStart()}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Erro ao buscar usuários');
    }
    return response.json();
  })
  .then(data => {
    console.log(data)
    return data;
  })
  .catch(error => {
    console.error(error);
    throw error;
  });
}

export function deleteUser(userId: string | undefined) {
  if(userId === undefined){
    throw new Error('Erro ao deletar usuário');
  }
  return fetch(`http://localhost:5000/delete/${userId}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  });
}

export async function updateUser(userId : string | undefined | string[], updatedUser:IUser) {
  const url = `http://localhost:5000/users/${userId}`; // Substitua "users" pelo endpoint correto da sua API

  try {
    const response = await fetch(url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updatedUser),
    });
    if (!response.ok) {
      throw new Error("Erro ao atualizar usuário");
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}
