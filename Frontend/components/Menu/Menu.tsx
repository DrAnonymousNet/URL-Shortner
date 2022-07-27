import React, { useState } from "react";
import Hamburger from "../Hamburger/Hamburger";
import Cross from "../Cross/Cross";
import MenuModal from "../MenuModal/MenuModal";

const Menu = () => {
  const [isModalActive, setIsModalActive] = useState(false);
  return (
    // essence of align-self: center; is to make the Hamburger/cross
    // icon to be positioned at the center of direct parent div
    <div className="relative flex flex-col justify-center">
      {isModalActive ? (
        <button onClick={() => setIsModalActive(false)}>
          <Cross />
        </button>
      ) : (
        <button onClick={() => setIsModalActive(true)}>
          <Hamburger  />
        </button>
      )}

      {isModalActive && (
        <div className="absolute right-0 w-max top-[160%] rounded-md overflow-hidden">
          <MenuModal setIsModalActive={setIsModalActive} />
        </div>
      )}
    </div>
  );
};

export default Menu;
