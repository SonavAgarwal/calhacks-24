"use client";

import {
	CellContext,
	ColumnDef,
	createColumnHelper,
	flexRender,
	getCoreRowModel,
	useReactTable,
} from "@tanstack/react-table";

import {
	Table,
	TableBody,
	TableCell,
	TableHead,
	TableHeader,
	TableRow,
} from "@/components/ui/table";
import { Item } from "@/lib/types";

interface ItemsTableProps<TData, TValue> {
	columns: ColumnDef<TData, TValue>[];
	data: TData[];
}

const itemsColumnHelper = createColumnHelper<Item>();
export const itemsColumns: ColumnDef<Item>[] = [
	{
		accessorKey: "id",
		header: "ID",
	},
	{
		accessorKey: "name",
		header: "Name",
	},
	{
		accessorKey: "price",
		header: "Price",
		accessorFn: (originalRow) => `$${originalRow.price.toFixed(2)}`,
	},
	{
		accessorKey: "quantity",
		header: "Quantity",
	},
	{
		accessorKey: "images",
		header: "Images",
		cell: (info: CellContext<Item, unknown>) => (
			<div className="flex space-x-2">
				{(info.getValue() as string[]).map((image) => (
					<img
						key={image}
						src={image}
						alt={info.row.original.name}
						className="w-10 h-10 object-cover rounded-md border-2 border-primary"
					/>
				))}
			</div>
		),
	},
	{
		accessorKey: "categories",
		header: "Categories",
	},
	{
		accessorKey: "dateUpdated",
		header: "Date Updated",
		accessorFn: (originalRow) => originalRow.dateUpdated.toLocaleDateString(),
	},
];

export function ItemsTable<TData, TValue>({
	columns,
	data,
}: ItemsTableProps<TData, TValue>) {
	const table = useReactTable({
		data,
		columns,
		getCoreRowModel: getCoreRowModel(),
	});

	return (
		<div className="rounded-md border">
			<Table>
				<TableHeader>
					{table.getHeaderGroups().map((headerGroup) => (
						<TableRow key={headerGroup.id}>
							{headerGroup.headers.map((header) => {
								return (
									<TableHead key={header.id}>
										{header.isPlaceholder
											? null
											: flexRender(
													header.column.columnDef.header,
													header.getContext()
											  )}
									</TableHead>
								);
							})}
						</TableRow>
					))}
				</TableHeader>
				<TableBody>
					{table.getRowModel().rows?.length ? (
						table.getRowModel().rows.map((row) => (
							<TableRow
								key={row.id}
								data-state={row.getIsSelected() && "selected"}
							>
								{row.getVisibleCells().map((cell) => (
									<TableCell key={cell.id}>
										{flexRender(cell.column.columnDef.cell, cell.getContext())}
									</TableCell>
								))}
							</TableRow>
						))
					) : (
						<TableRow>
							<TableCell colSpan={columns.length} className="h-24 text-center">
								No results.
							</TableCell>
						</TableRow>
					)}
				</TableBody>
			</Table>
		</div>
	);
}
