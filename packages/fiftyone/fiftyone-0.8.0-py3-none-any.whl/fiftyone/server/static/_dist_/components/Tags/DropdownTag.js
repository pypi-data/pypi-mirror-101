import React, {useRef, useState} from "../../../_snowpack/pkg/react.js";
import styled from "../../../_snowpack/pkg/styled-components.js";
import {Button, Popper} from "../../../_snowpack/pkg/@material-ui/core.js";
import {ArrowDropDown} from "../../../_snowpack/pkg/@material-ui/icons.js";
import Menu from "../Menu.js";
import SelectionTag from "./SelectionTag.js";
import {useOutsideClick} from "../../utils/hooks.js";
const Container = styled.div`
  cursor: ${({disabled}) => disabled ? "not-allowed" : void 0};

  .dropdown-button {
    padding-left: 0;
    padding-right: 0;

    .dropdown-icon {
      color: ${({theme, disabled}) => disabled ? theme.fontDarkest : void 0};
    }
  }

  .popper {
    z-index: ${({menuZIndex}) => menuZIndex};
  }
`;
const Body = styled(SelectionTag.Body)`
  display: flex;
  align-items: center;
  text-transform: none;
  padding-right: 0.5em;
`;
const DropdownTag = React.memo(({
  name,
  menuItems,
  menuZIndex = 1,
  disabled = false,
  title,
  onSelect,
  onOpen = () => {
  },
  onClose = () => {
  },
  ...rest
}) => {
  const [isOpen, setOpen] = useState(false);
  const anchorRef = useRef(null);
  const containerRef = useRef(null);
  const handleToggle = () => {
    setOpen(!isOpen);
    if (isOpen) {
      onClose();
    } else {
      onOpen();
    }
  };
  const handleClose = () => {
    onClose();
  };
  const handleSelect = (item) => {
    onSelect(item);
    setOpen(false);
  };
  useOutsideClick(containerRef, () => {
    setOpen(false);
  });
  return /* @__PURE__ */ React.createElement(Container, {
    menuZIndex,
    disabled,
    title
  }, /* @__PURE__ */ React.createElement(Button, {
    classes: {root: "dropdown-button"},
    ref: anchorRef,
    onClick: handleToggle,
    disabled
  }, /* @__PURE__ */ React.createElement(Body, {
    disabled,
    ...rest
  }, name, " ", /* @__PURE__ */ React.createElement(ArrowDropDown, {
    className: "dropdown-icon"
  }))), /* @__PURE__ */ React.createElement(Popper, {
    open: isOpen,
    anchorEl: anchorRef.current,
    role: void 0,
    transition: true,
    disablePortal: true,
    className: "popper",
    ref: containerRef
  }, /* @__PURE__ */ React.createElement(Menu, {
    autoFocusItem: isOpen,
    items: menuItems,
    onClose: handleClose,
    onSelect: handleSelect
  })));
});
DropdownTag.Body = Body;
export default DropdownTag;
