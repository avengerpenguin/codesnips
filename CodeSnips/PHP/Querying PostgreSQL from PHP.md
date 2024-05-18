```php
<?php
// Database configuration
$host = 'localhost';
$dbname = 'your_database_name';
$user = 'your_username';
$password = 'your_password';

try {
    // Create a new PDO instance
    $pdo = new PDO("pgsql:host=$host;dbname=$dbname", $user, $password);

    // Set the PDO error mode to exception
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Prepare and execute a SELECT query
    $query = "SELECT * FROM your_table_name";
    $stmt = $pdo->prepare($query);
    $stmt->execute();

    // Fetch results as an associative array
    $results = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Loop through results and display data
    foreach ($results as $row) {
        echo "ID: " . $row['id'] . ", Name: " . $row['name'] . "<br>";
    }
} catch (PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
}
?>
```
