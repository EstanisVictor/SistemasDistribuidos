import { ButtonPrimary, EnhancedTable, Nav } from "components";
import { useRouter } from "next/router";

export default function Tabela() {

  const router = useRouter();

  const handleClick = () => {
    router.push('/')
  };

  return(
    <>
    <Nav />
    <h1 className='text-center text-3xl mt-10 mb-7'>Informações</h1>
    <div className="flex items-center flex-col justify-center w-full">
      <EnhancedTable />
      <ButtonPrimary onClick={handleClick}>Voltar</ButtonPrimary>
    </div>
    </>
  );
}