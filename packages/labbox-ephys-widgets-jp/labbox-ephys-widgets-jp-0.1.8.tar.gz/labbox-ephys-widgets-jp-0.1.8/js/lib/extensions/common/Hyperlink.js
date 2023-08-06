import React from 'react';
const Hyperlink = ({ color, onClick, children }) => {
    let style0 = {
        color: color || 'gray',
        cursor: 'pointer',
        textDecoration: 'underline'
    };
    return (React.createElement("span", { style: style0, onClick: onClick }, children));
};
export default Hyperlink;
//# sourceMappingURL=Hyperlink.js.map