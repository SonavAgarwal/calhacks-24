import {
	CellContext,
	ColumnDef,
	createColumnHelper,
} from "@tanstack/react-table";

export interface Item {
	id: number;
	name: string;
	price: number;
	quantity: number;
	images: string[]; // URLs
	categories: string[];
	dateUpdated: Date;
}

export interface Claim {
	id: number;
	name: string;
	dateFiled: Date;
	items: Item[];
}
