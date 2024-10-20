"use client"

import React, { useEffect, useState } from "react"
import ReactPDF, {
    Page,
    Text,
    View,
    Document,
    StyleSheet,
    PDFViewer,
    Image,
} from "@react-pdf/renderer"
import { Item } from "@/lib/types"

// Create styles
const styles = StyleSheet.create({
    page: {
        padding: 20,
    },
    table: {
        // display: "table",
        width: "auto",
    },
    tableRow: {
        flexDirection: "row",
    },
    tableCell: {
        flex: 1,
        padding: 5,
        fontSize: 10,
        borderBottomWidth: 1,
        borderColor: "#000",
    },
})

const items = [
    {
        category: "Electronics",
        item: "Laptop",
        description: "MacBook Pro",
        yearBought: "2020",
        qty: 1,
        replacementCost: "$1500",
        totalCost: "$1500",
        link: "https://example.com/laptop",
        picture: "https://picsum.photos/200/300",
    },
    {
        category: "Electronics",
        item: "Laptop",
        description: "MacBook Pro",
        yearBought: "2020",
        qty: 1,
        replacementCost: "$1500",
        totalCost: "$1500",
        link: "https://example.com/laptop",
        picture: "https://picsum.photos/200/300",
    },
    {
        category: "Electronics",
        item: "Laptop",
        description: "MacBook Pro",
        yearBought: "2020",
        qty: 1,
        replacementCost: "$1500",
        totalCost: "$1500",
        link: "https://example.com/laptop",
        picture: "https://picsum.photos/200/300",
    },
    // More items...
]

// Create Document Component
const MyDocument = () => {
    // const data = items

    const [data, setData] = useState<Item[]>([])
    useEffect(() => {
        // load "claimedItems" from localStorage
        const items = JSON.parse(localStorage.getItem("claimedItems") || "[]")
        setData(items)
    }, [])

    console.log(data)
    return (
        <Document>
            <Page size="A4" orientation="landscape" style={styles.page}>
                <View style={styles.table}>
                    {/* Table Headers */}
                    <View style={styles.tableRow}>
                        <Text style={styles.tableCell}>Category</Text>
                        <Text style={styles.tableCell}>Item</Text>
                        <Text style={{ ...styles.tableCell, flexGrow: 2 }}>
                            Description
                        </Text>
                        <Text style={styles.tableCell}>Year Bought</Text>
                        <Text style={styles.tableCell}>Qty</Text>
                        <Text style={styles.tableCell}>Replacement Cost</Text>
                        <Text style={styles.tableCell}>Total Cost</Text>
                        <Text
                            style={{
                                ...styles.tableCell,
                                flexGrow: 3,
                            }}
                        >
                            Link
                        </Text>
                        {/* <Text style={styles.tableCell}>Picture</Text> */}
                    </View>

                    {/* Table Rows - Loop through data */}
                    {data.map((item, index) => (
                        <View key={index} style={styles.tableRow}>
                            <Text style={styles.tableCell}>
                                {item.category}
                            </Text>
                            <Text style={styles.tableCell}>{item.name}</Text>
                            <Text style={{ ...styles.tableCell, flexGrow: 2 }}>
                                {item.description}
                            </Text>
                            <Text style={styles.tableCell}>{2024}</Text>
                            <Text style={styles.tableCell}>{item.count}</Text>
                            <Text style={styles.tableCell}>{item.price}</Text>
                            <Text style={styles.tableCell}>{item.price}</Text>
                            <Text
                                style={{
                                    ...styles.tableCell,
                                    flexGrow: 3,
                                }}
                            >
                                https://example.com/{item.name}
                            </Text>
                            {/* <Image
                                style={styles.tableCell}
                                src={item.picture}
                            /> */}
                        </View>
                    ))}
                </View>
            </Page>
        </Document>
    )
}

const page = () => {
    const [isClient, setIsClient] = useState(false)

    useEffect(() => {
        setIsClient(true)
    }, [])

    if (!isClient) {
        return null
    }
    return (
        <PDFViewer
            style={{
                width: "100%",
                height: "100vh",
                border: "none",
            }}
        >
            <MyDocument />
        </PDFViewer>
    )
}

export default page
