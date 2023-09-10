import { IUser } from "Interfaces";
import { Api } from "providers";


export function createUser(user: IUser) {
  // return Api.post<any>("/generate", user);
  return fetch("http://localhost:8080/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(user),
  })
}

export function getAllUsers() {
  return fetch("http://localhost:8080/getAll", {
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
  return fetch(`http://localhost:8080/getUser/${userID?.trimEnd().trimStart()}`, {
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
    return data["data"];
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
  return fetch(`http://localhost:8080/delete/${userId}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  });
}

export async function updateUser(userId : string | undefined | string[], updatedUser:IUser) {
  const url = `http://localhost:8080/users/${userId}`; // Substitua "users" pelo endpoint correto da sua API
  console.log("url: "+updatedUser);
  
  try {
    const response = await fetch(url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updatedUser),
    });

    if (!response.ok) {
      const errorMessage = `Erro ao atualizar usuário: ${response.statusText}`;
      throw new Error(errorMessage);
    }
    // const data = await response.json();
    return response;
  } catch (error) {
    console.error(error);
    throw error;
  }
}
