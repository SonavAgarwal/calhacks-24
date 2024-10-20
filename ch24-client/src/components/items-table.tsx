"use client"

import { flexRender, useReactTable } from "@tanstack/react-table"

import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import { Item } from "@/lib/types"
import { Fragment } from "react"
import { fixBoolean } from "@/lib/misc"

interface ItemsTableProps<Item> {
    data: Item[]
    table: ReturnType<typeof useReactTable<Item>>
    onRowClick: (item: Item) => void
    expandedRow?: Item | null
}

export function ItemsTable<Items>({
    data,
    table,
    onRowClick,
    expandedRow,
}: ItemsTableProps<Item>) {
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
                                                  header.column.columnDef
                                                      .header,
                                                  header.getContext(),
                                              )}
                                    </TableHead>
                                )
                            })}
                        </TableRow>
                    ))}
                </TableHeader>
                <TableBody>
                    {table.getRowModel().rows?.length ? (
                        table.getRowModel().rows.map((row, index) => (
                            <Fragment key={`fragment-${row.id}-${index}`}>
                                <TableRow
                                    key={`row-${row.id}-${index}`}
                                    data-state={
                                        row.getIsSelected() && "selected"
                                    }
                                    onClick={() => {
                                        onRowClick(row.original)
                                    }}
                                >
                                    {row.getVisibleCells().map((cell) => (
                                        <TableCell key={cell.id}>
                                            {flexRender(
                                                cell.column.columnDef.cell,
                                                cell.getContext(),
                                            )}
                                        </TableCell>
                                    ))}
                                </TableRow>
                                {expandedRow === row.original && (
                                    <TableRow
                                        key={`${row.id}-expanded`}
                                        data-state="expanded"
                                    >
                                        <TableCell
                                            colSpan={
                                                row.getVisibleCells().length
                                            }
                                        >
                                            <div className="flex flex-col">
                                                <div className="flex flex-row justify-center gap-4">
                                                    {/* find an image where status is inventory and before is true */}
                                                    {row.original.images
                                                        ?.filter((image) =>
                                                            // image.status ===
                                                            //     "inventory"
                                                            //      &&
                                                            fixBoolean(
                                                                image.before,
                                                            ),
                                                        )
                                                        ?.slice(0, 1)
                                                        ?.map((image) => (
                                                            <div
                                                                key={
                                                                    image.url_path
                                                                }
                                                                className="flex h-full flex-col items-center gap-2 rounded-lg border bg-white p-4"
                                                            >
                                                                <img
                                                                    key={
                                                                        image.url_path
                                                                    }
                                                                    src={
                                                                        image.url_path
                                                                    }
                                                                    className="h-64 flex-1 rounded-lg object-cover"
                                                                />
                                                                <h3 className="text-base">
                                                                    Before
                                                                </h3>
                                                            </div>
                                                        ))}

                                                    {/* find an image  where before is false */}
                                                    {row.original.images
                                                        ?.filter(
                                                            (image) =>
                                                                !fixBoolean(
                                                                    image.before,
                                                                ),
                                                        )
                                                        ?.slice(0, 1)
                                                        ?.map((image) => (
                                                            <div
                                                                key={
                                                                    image.url_path
                                                                }
                                                                className="flex h-full flex-col items-center gap-2 rounded-lg border bg-white p-4"
                                                            >
                                                                <img
                                                                    key={
                                                                        image.url_path
                                                                    }
                                                                    src={
                                                                        image.url_path
                                                                    }
                                                                    className="h-64 flex-1 rounded-lg object-cover"
                                                                />
                                                                <h3 className="text-base">
                                                                    After
                                                                </h3>
                                                            </div>
                                                        ))}
                                                </div>
                                            </div>
                                        </TableCell>
                                    </TableRow>
                                )}
                            </Fragment>
                        ))
                    ) : (
                        <TableRow>
                            <TableCell
                                colSpan={table?.getAllColumns()?.length}
                                className="h-24 text-center"
                            >
                                No results.
                            </TableCell>
                        </TableRow>
                    )}
                </TableBody>
            </Table>
        </div>
    )
}
