import * as yup from "yup";
import { useForm } from "react-hook-form";
import { Inter } from 'next/font/google'
import { ButtonPrimary, Nav } from 'components'
import { useRouter } from 'next/router';
import Link from 'next/link';
import { yupResolver } from "@hookform/resolvers/yup";
import { createUser } from "Services";

const inter = Inter({ subsets: ['latin'] })

type InputType = {
  name: string;
  email: string;
};

export default function Home() {

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

  const handleSubmitForm = handleSubmit(async (data: InputType) => {
    console.log(data);
    
    await createUser(data);
    router.push('/tabela')
  });

  const handleClick = () => {
    router.push('/tabela')
  };

  return (
    <>
    <Nav />
      <div className='flex items-center justify-center'>
        <form onSubmit={handleSubmitForm} className='items-center w-full mt-5 flex justify-center flex-col gap-2 bg-white p-2 border border-solid border-gray-150 max-w-md'>
            <h3 className='text-center '>Bem Vindo</h3>
            <label className='flex flex-col w-full'>
              <span>Nome</span>
              <input {...register("name")} className='p-2 rounded-md border-gray-400 border-solid border-2 enabled:hover:border-blue-500 focus:border-blue-700 outline-none' type="text"/>
              {errors.name && <p className="text-red-600 text-sm font-mono">{errors.name.message}</p>}
            </label>
            <label className='flex flex-col w-full'>
              <span>Email</span>
              <input {...register("email")}  type='email' className='p-2 rounded-md border-gray-400 border-solid border-2 enabled:hover:border-blue-500 focus:border-blue-700 outline-none'/>
              {errors.email && <p className="text-red-600 text-sm font-mono">{errors.email.message}</p>}
            </label>
            <ButtonPrimary>Enviar</ButtonPrimary>
        </form>
      </div>
      <Link href='/tabela' className='flex items-center justify-center mt-4'>
        <ButtonPrimary onClick={handleClick} >Ir para Tabela</ButtonPrimary>
      </Link>
    </>
  )
}
