import React from "../../_snowpack/pkg/react.js";
import styled from "../../_snowpack/pkg/styled-components.js";
import {
  ClickAwayListener,
  Divider,
  MenuItem,
  MenuList
} from "../../_snowpack/pkg/@material-ui/core.js";
const Container = styled.div`
  .menu {
    background-color: ${({theme}) => theme.menuBackground};
    border: 2px solid ${({theme}) => theme.menuBorder};
    box-shadow: 0 2px 20px 0 ${({theme}) => theme.darkerShadow};

    .item {
      color: ${({theme}) => theme.fontDark};
      font-family: unset;
      font-weight: bold;
      font-size: 14px;
      line-height: 29px;
      padding-top: 0;
      padding-bottom: 0;
    }

    .divider {
      height: 2px;
      background-color: ${({theme}) => theme.menuBorder};
      margin: 3px 0;
    }
  }
`;
const Menu = ({items, onClose, onSelect, ...rest}) => {
  return /* @__PURE__ */ React.createElement(Container, null, /* @__PURE__ */ React.createElement(ClickAwayListener, {
    onClickAway: onClose
  }, /* @__PURE__ */ React.createElement(MenuList, {
    classes: {root: "menu"},
    ...rest
  }, items.map((item, i) => item === Menu.DIVIDER ? /* @__PURE__ */ React.createElement(Divider, {
    key: i,
    classes: {root: "divider"}
  }) : /* @__PURE__ */ React.createElement(MenuItem, {
    key: i,
    disabled: item.disabled,
    onClick: () => onSelect(item),
    classes: {root: "item"}
  }, item.name)))));
};
Menu.DIVIDER = "-";
export default Menu;
