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
                    SpeciesId= 183086,
                    CommonName = "European mountain ash",
                    ImageUrl= "https://bs.floristic.org/image/o/63073d2fbf45b90701279405ecc2eec0272906ed",
                    DatePlanted = "",
                    DateHarvested = "",
                    LastWatering = "",
                    HealthStatus="", 
                    SoilPH=7, 
                    Light=10, 
                    SoilMoisture=0, 
                    AmountHarvested=0,
                    GardenerId=1,
                }
            );
        }
        public DbSet<Plant> Plants { get; set; }
    }
}
