import {
	CellContext,
	ColumnDef,
	createColumnHelper,
} from "@tanstack/react-table";
import { Claim, Item } from "./types";

export const items: Item[] = [
	{
		id: 1,
		name: "Chair",
		price: 100,
		quantity: 2,
		images: [
			"https://target.scene7.com/is/image/Target/GUEST_2438430f-ffdb-4fd8-95a6-d7cc7389f7ad",
		],
		categories: ["furniture"],
		dateUpdated: new Date("2021-01-01"),
	},
	{
		id: 2,
		name: "Desk",
		price: 200,
		quantity: 1,
		images: [
			"https://target.scene7.com/is/image/Target/GUEST_2438430f-ffdb-4fd8-95a6-d7cc7389f7ad",
		],
		categories: ["furniture"],
		dateUpdated: new Date("2021-01-02"),
	},
	{
		id: 3,
		name: "Lamp",
		price: 50,
		quantity: 3,
		images: [
			"https://target.scene7.com/is/image/Target/GUEST_2438430f-ffdb-4fd8-95a6-d7cc7389f7ad",
		],
		categories: ["lighting"],
		dateUpdated: new Date("2021-01-03"),
	},
];

export const claims: Claim[] = [
	{
		id: 1,
		name: "John Doe",
		dateFiled: new Date("2021-01-01"),
		items: [items[0], items[1]],
	},
	{
		id: 2,
		name: "Jane Doe",
		dateFiled: new Date("2021-01-02"),
		items: [items[2]],
	},
];
