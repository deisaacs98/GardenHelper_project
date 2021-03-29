using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Text;
using GardenHelperWebAPI.Models;

namespace GardenHelperWebAPI.Data
{
    public class ApplicationDbContext : IdentityDbContext
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
                new Gardener { Id = 1, FirstName="John", MiddleInitial="J", LastName="Gardener", 
                               AddressLine1="", AddressLine2="", City="", State="", Zip=90210, 
                                Email="", Phone = 0, Lat=0, Lng=0, Garden=null}
                

            );
        }


        public DbSet<Gardener> Gardeners { get; set; }
    }
}
