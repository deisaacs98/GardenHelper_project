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
            modelBuilder.Entity<Gardener>().HasData(
                new Gardener
                {
                    Id = 1,
                    FirstName = "John",
                    MiddleInitial = "J",
                    LastName = "Gardener",
                    AddressLine1 = "",
                    AddressLine2 = "",
                    City = "",
                    State = "",
                    Zip = 90210,
                    Email = "",
                    Phone = 0,
                    Lat = 0,
                    Lng = 0
                }
            );
            modelBuilder.Entity<Plant>().HasData(
                new Plant { Id=1, 
                    CommonName="",
                    DatePlanted=new System.DateTime(2020-3-28),
                    DateHarvested = new System.DateTime(2020 - 3 - 29),
                    LastWatering = new System.DateTime(2020 - 3 - 28),
                    HealthStatus="", 
                    SoilPH=7, 
                    Light=10, 
                    SoilMoisture=0, 
                    AmountHarvested=0,
                    GardenerId=1,
                }
            );
        }

        public DbSet<Gardener> Gardeners { get; set; }
        public DbSet<Plant> Plants { get; set; }
    }
}
