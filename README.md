Para abordar la refactorización del sistema de reservas de hotel aplicando los patrones de diseño GoF sugeridos (Factory Method, Strategy, Singleton, y Observer), vamos a descomponer las responsabilidades y mejorar el código para hacerlo más escalable y mantenible.

### 1. **Factory Method** (para la creación de habitaciones)
Vamos a encapsular la creación de diferentes tipos de habitaciones dentro de un método fábrica, lo que nos permitirá agregar nuevos tipos de habitaciones sin cambiar el código del sistema.

### 2. **Strategy Pattern** (para la lógica de reserva)
Aplicaremos el patrón Strategy para manejar diferentes tipos de reservas, como reservas estándar y VIP, permitiendo la extensión sin modificar el código existente.

### 3. **Singleton** (para la clase `Hotel`)
El patrón Singleton será útil para garantizar que solo exista una instancia de `Hotel` en el sistema.

### 4. **Observer Pattern** (para notificar cambios en las reservas)
Implementaremos el patrón Observer para que otros componentes, como el servicio de limpieza o el sistema de facturación, puedan suscribirse a eventos de reservas.

### Refactorización del Código:

```csharp
using System;
using System.Collections.Generic;

// Singleton para la clase Hotel
public class Hotel
{
    private static Hotel _instance;
    public string Name { get; set; }
    public List<Room> Rooms { get; private set; } = new List<Room>();

    private Hotel() { }

    public static Hotel Instance
    {
        get
        {
            if (_instance == null)
                _instance = new Hotel();
            return _instance;
        }
    }

    public void AddRoom(IRoomFactory roomFactory)
    {
        Room room = roomFactory.CreateRoom();
        Rooms.Add(room);
    }

    public void PrintAvailableRooms()
    {
        foreach (var room in Rooms)
        {
            Console.WriteLine($"Room: {room.RoomType}, Price: {room.Price}");
        }
    }
}

// Clase abstracta Room
public class Room
{
    public string RoomType { get; set; }
    public double Price { get; set; }
}

// Factory Method para la creación de habitaciones
public interface IRoomFactory
{
    Room CreateRoom();
}

public class SingleRoomFactory : IRoomFactory
{
    public Room CreateRoom()
    {
        return new Room { RoomType = "Single", Price = 100 };
    }
}

public class DoubleRoomFactory : IRoomFactory
{
    public Room CreateRoom()
    {
        return new Room { RoomType = "Double", Price = 200 };
    }
}

// Strategy Pattern para diferentes tipos de reservas
public interface IReservationStrategy
{
    void MakeReservation(Hotel hotel, string roomType, DateTime startDate, DateTime endDate);
}

public class StandardReservation : IReservationStrategy
{
    public void MakeReservation(Hotel hotel, string roomType, DateTime startDate, DateTime endDate)
    {
        var room = hotel.Rooms.Find(r => r.RoomType == roomType);
        if (room != null)
        {
            Console.WriteLine($"Standard Reservation made for {room.RoomType} from {startDate} to {endDate}.");
            // Notificar observadores
            ReservationNotifier.Notify(room, startDate, endDate);
        }
        else
        {
            Console.WriteLine("Room not available.");
        }
    }
}

// Observer Pattern para notificar cambios en las reservas
public interface IReservationObserver
{
    void Update(Room room, DateTime startDate, DateTime endDate);
}

public class CleaningService : IReservationObserver
{
    public void Update(Room room, DateTime startDate, DateTime endDate)
    {
        Console.WriteLine($"Cleaning service notified for room {room.RoomType} reservation from {startDate} to {endDate}.");
    }
}

public class ReservationNotifier
{
    private static List<IReservationObserver> _observers = new List<IReservationObserver>();

    public static void Attach(IReservationObserver observer)
    {
        _observers.Add(observer);
    }

    public static void Notify(Room room, DateTime startDate, DateTime endDate)
    {
        foreach (var observer in _observers)
        {
            observer.Update(room, startDate, endDate);
        }
    }
}

class Program
{
    static void Main(string[] args)
    {
        // Singleton para la instancia de Hotel
        var hotel = Hotel.Instance;
        hotel.Name = "Luxury Inn";

        // Creación de habitaciones con Factory Method
        hotel.AddRoom(new SingleRoomFactory());
        hotel.AddRoom(new DoubleRoomFactory());

        // Observer: Servicio de limpieza se suscribe a las reservas
        CleaningService cleaningService = new CleaningService();
        ReservationNotifier.Attach(cleaningService);

        // Strategy Pattern para la reserva estándar
        IReservationStrategy reservationStrategy = new StandardReservation();
        reservationStrategy.MakeReservation(hotel, "Single", DateTime.Now, DateTime.Now.AddDays(2));

        hotel.PrintAvailableRooms();
    }
}
```

### Explicación de los cambios:

- **Singleton Pattern**: `Hotel` se implementa como Singleton para asegurar que solo exista una instancia de la clase en todo el sistema.
  
- **Factory Method**: Hemos utilizado el Factory Method para encapsular la creación de diferentes tipos de habitaciones, como `SingleRoomFactory` y `DoubleRoomFactory`. Esto facilita la extensión sin cambiar el código base.

- **Strategy Pattern**: Implementamos el patrón Strategy en la clase `ReservationStrategy`, lo que nos permite manejar diferentes tipos de reservas sin modificar el código base.

- **Observer Pattern**: Los observadores, como `CleaningService`, son notificados cuando se realiza una nueva reserva. Esto se logra utilizando el patrón Observer.

### Beneficios:
- **Desacoplamiento**: Las clases ahora están mejor organizadas y desacopladas, facilitando la mantenibilidad y escalabilidad.
- **Flexibilidad**: Añadir nuevos tipos de habitaciones o estrategias de reserva no requiere cambios en las clases existentes.
- **Notificaciones**: El sistema ahora puede notificar automáticamente a servicios externos, como el servicio de limpieza, cuando se realiza una nueva reserva.

Este enfoque sigue los principios SOLID, mejorando la estructura y la claridad del código.

