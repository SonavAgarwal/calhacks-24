import React from "react";

const layout = (props: { children: React.ReactNode }) => {
	return (
		<div className="w-screen min-h-screen flex flex-col items-center">
			<div className="w-[48rem] min-h-screen flex flex-col">
				{props.children}
			</div>
		</div>
	);
};

export default layout;
