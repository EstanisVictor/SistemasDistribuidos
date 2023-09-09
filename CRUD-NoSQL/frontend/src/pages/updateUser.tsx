import { yupResolver } from "@hookform/resolvers/yup";
import { ButtonPrimary, Nav } from "components";
import { useRouter } from "next/router";
import * as yup from "yup";
import { useForm } from "react-hook-form";
import Link from "next/link";
import { updateUser } from "Services";

type InputType = {
  name: string;
  email: string;
};

export default function UpdateUser() {

  const schema = yup.object().shape({
    name: yup.string().required("Nome é obrigatório"),
    email: yup.string().required("Email é obrigatório"),
  });

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<InputType>({
    resolver: yupResolver(schema),
  });

  const router = useRouter();
  
  const {id, name, email} = router.query;

  const handleClickTable = () => {
    router.push('/tabela')
  };

  const handleClickCadastro = () => {
    router.push('/')
  };

  const handleSubmitForm = handleSubmit(async (data: InputType) => {
    await updateUser(id, data);
    router.push('/tabela')
  });

  return (
    <>
    <Nav />
    <h1 className='flex items-center justify-center text-4xl text-primaryDark'>Update</h1>
      <div className='flex items-center justify-center'>
        <form onSubmit={handleSubmitForm} className='items-center w-full mt-5 flex justify-center flex-col gap-2 bg-white p-2 border border-solid border-gray-150 max-w-md'>
            <h3 className='text-center '>Atualizar os dados</h3>
            <label className='flex flex-col w-full'>
              <span>Nome</span>
              <span className="border mb-3 mt-3 rounded-lg border-red-600 text-center text-red-600">{name}</span>
              <input {...register("name")} className='p-2 rounded-md border-gray-400 border-solid border-2 enabled:hover:border-blue-500 focus:border-blue-700 outline-none' type="text"/>
              {errors.name && <p className="text-red-600 text-sm font-mono">{errors.name.message}</p>}
            </label>
            <label className='flex flex-col w-full'>
              <span>Email</span>
              <span className="border mb-3 mt-3 rounded-lg border-red-600 text-center text-red-600">{email}</span>
              <input {...register("email")}  type='email' className='p-2 rounded-md border-gray-400 border-solid border-2 enabled:hover:border-blue-500 focus:border-blue-700 outline-none'/>
              {errors.email && <p className="text-red-600 text-sm font-mono">{errors.email.message}</p>}
            </label>
            <ButtonPrimary>Atualizar</ButtonPrimary>
        </form>
      </div>
      <div className="mt-4 items-center flex justify-center">
        <div className="mr-2 ml-2">
          <ButtonPrimary onClick={handleClickTable} >Ir para tabela</ButtonPrimary>
        </div>
        <div className="mr-2 ml-2">
          <ButtonPrimary onClick={handleClickCadastro} >Ir para cadastro</ButtonPrimary>
        </div>
      </div>
      
    </>
  )
}