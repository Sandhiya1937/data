<?php
// Handle adding new items
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['item_name'])) {
    $itemName = $_POST['item_name'];
    $itemQuantity = $_POST['item_quantity'];
    $itemPrice = $_POST['item_price'];

    $inventoryFile = 'inventory.json';
    $inventory = [];

    if (file_exists($inventoryFile)) {
        $inventory = json_decode(file_get_contents($inventoryFile), true);
    }

    $newItem = [
        'id' => count($inventory) + 1,
        'name' => $itemName,
        'quantity' => $itemQuantity,
        'price' => $itemPrice,
    ];

    $inventory[] = $newItem;
    file_put_contents($inventoryFile, json_encode($inventory));

    header('Location: ' . $_SERVER['PHP_SELF']);
    exit();
}

// Simulate a QR scan
if (isset($_GET['scan'])) {
    $scannedItem = [
        'id' => 1,
        'name' => 'Sample Item',
        'quantity' => 10,
        'price' => 25.99,
    ];

    header('Location: ' . $_SERVER['PHP_SELF'] . '?scanned_item=' . urlencode(json_encode($scannedItem)));
    exit();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inventory Management System</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
<style>
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 20px;
        background-color: #f5f5f5;
    }
    header {
        background-color: #333;
        color: white;
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 5px;
    }
    section {
        background-color: white;
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th, td {
        padding: 10px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }
    th {
        background-color: #f2f2f2;
    }
    input, button {
        padding: 8px;
        margin: 5px 5px 5px 0;
        border: 1px solid #ddd;
        border-radius: 4px;
    }
    button {
        background-color: #4CAF50;
        color: white;
        cursor: pointer;
    }
    button:hover {
        background-color: #45a049;
    }
    #qr-result {
        margin-top: 15px;
        padding: 10px;
        background-color: #f9f9f9;
        border-radius: 4px;
    }
</style>
    <header>
        <h1>Inventory Management System</h1>
    </header>

    <section id="inventory">
        <h2>Inventory</h2>
        <table id="inventory-table">
            <thead>
                <tr>
                    <th>Item ID</th>
                    <th>Product Name</th>
                    <th>Quantity</th>
                    <th>Price</th>
                    <th>QR Code</th>
                </tr>
            </thead>
            <tbody>
                <?php
                // Fetch inventory data
                $inventoryFile = 'inventory.json';
                if (file_exists($inventoryFile)) {
                    $inventory = json_decode(file_get_contents($inventoryFile), true);
                    foreach ($inventory as $item) {
                        echo "<tr>
                            <td>{$item['id']}</td>
                            <td>{$item['name']}</td>
                            <td>{$item['quantity']}</td>
                            <td>\${$item['price']}</td>
                            <td><img src='https://api.qrserver.com/v1/create-qr-code/?data=" . urlencode(json_encode($item)) . "&size=100x100' alt='QR Code'></td>
                        </tr>";
                    }
                }
                ?>
            </tbody>
        </table>
    </section>

    <section id="add-item">
        <h2>Add New Item</h2>
        <form method="POST" action="">
            <input type="text" name="item_name" placeholder="Product Name" required>
            <input type="number" name="item_quantity" placeholder="Quantity" required>
            <input type="number" name="item_price" placeholder="Price" required>
            <button type="submit">Add Item</button>
        </form>
    </section>

    <section id="scan-qr">
        <h2>Scan QR Code</h2>
        <form method="GET" action="">
            <button type="submit" name="scan">Simulate QR Scan</button>
        </form>
        <div id="qr-result">
            <?php
            // Display scanned QR result
            if (isset($_GET['scanned_item'])) {
                $scannedItem = json_decode($_GET['scanned_item'], true);
                echo "<h3>Scanned Item:</h3>
                    <p>Product: {$scannedItem['name']}</p>
                    <p>Quantity: {$scannedItem['quantity']}</p>
                    <p>Price: \${$scannedItem['price']}</p>";
            } else {
                echo "<p>No QR code scanned yet.</p>";
            }
            ?>
        </div>
    </section>
</body>
</html>