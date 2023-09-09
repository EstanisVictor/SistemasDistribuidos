type props = {
  children: React.ReactNode;
  onClick?: () => void;
};


export function ButtonPrimary({children, onClick}:props){
  return(
    <button type="submit" onClick={onClick} className="py-2 px-4 rounded-md bg-primaryLight hover:bg-primaryDark hover:text-white active:bg-blue-950">
      {children}
    </button>
  );
};