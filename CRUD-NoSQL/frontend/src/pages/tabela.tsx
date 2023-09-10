import { ButtonPrimary, EnhancedTable, Nav } from "components";
import { useRouter } from "next/router";

export default function Tabela() {

  const router = useRouter();

  const handleClick = () => {
    router.push('/')
  };

  const handleClickRefresh = () => {
    window.location.reload();
  };

  return(
    <>
    <Nav />
    <h1 className='text-center text-3xl mt-10 mb-7'>Informações</h1>
    <div className="flex items-center flex-col justify-center w-full">
      <EnhancedTable />
      <div className="flex">
        <span className="ml-2 mr-2"><ButtonPrimary onClick={handleClick}>Voltar</ButtonPrimary></span>
        <span className="ml-2 mr-2"><ButtonPrimary onClick={handleClickRefresh}>Refresh</ButtonPrimary></span>
      </div>
    </div>
    </>
  );
}