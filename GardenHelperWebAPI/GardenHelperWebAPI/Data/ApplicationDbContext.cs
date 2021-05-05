using Microsoft.EntityFrameworkCore;
using GardenHelperWebAPI.Models;

namespace GardenHelperWebAPI.Data
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);
            // Seed data - needs migration
            modelBuilder.Entity<Plant>().HasData(
                new Plant { Id=1, 
                    SpeciesId= 183722,
                    CommonName = "Spinach",
                    ImageUrl= "https://bs.plantnet.org/image/o/3cc08d812a893df9a574b1d377dc5b7c4d6477bc",
                    DatePlanted = "",
                    LastWatering = "",
                    HealthStatus="Good", 
                    Height = 10,
                    SoilPH = 7, 
                    Light = 7, 
                    SoilMoisture=0,
                    Edible = true,
                    MinTemp = null,
                    MaxTemp = null,
                    MinPH = 7.0,
                    MaxPH = 7.5,
                    RequiredLight = 7,
                    MinPrecipitation = null,
                    MaxPrecipitation = null,
                    AtmosphericHumidity = 5,
                    SoilHumidity = null,
                    GardenerId =1,
                }
            );
            modelBuilder.Entity<Log>().HasData(
                new Log
                {
                    Id = 1,
                    PlantId=1,
                    Date = "",
                    ImageUrl = "https://bs.floristic.org/image/o/63073d2fbf45b90701279405ecc2eec0272906ed",
                    WateredToday=true,
                    HealthStatus = "",
                    Height = 10,
                    SoilPH = 7,
                    Light = 10,
                    SoilMoisture = 0,
                    WaterPrediction=true,
                    PredictionAccurate=true
                }
            );
            modelBuilder.Entity<EdibleLog>().HasData(
                new EdibleLog
                {
                    Id = 1,
                    PlantId = 1,
                    Date = "",
                    Harvested = true,
                    DaysToHarvest = 2,
                    AmountHarvested = 10
                }
            );
        }
        public DbSet<Plant> Plants { get; set; }
        public DbSet<Log> Logs { get; set; }
        public DbSet<EdibleLog> EdibleLogs { get; set; }
    }
}
