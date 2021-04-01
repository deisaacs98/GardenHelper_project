﻿// <auto-generated />
using GardenHelperWebAPI.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Metadata;
using Microsoft.EntityFrameworkCore.Migrations;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;

namespace GardenHelperWebAPI.Migrations
{
    [DbContext(typeof(ApplicationDbContext))]
    [Migration("20210401155110_Init")]
    partial class Init
    {
        protected override void BuildTargetModel(ModelBuilder modelBuilder)
        {
#pragma warning disable 612, 618
            modelBuilder
                .HasAnnotation("ProductVersion", "3.0.1")
                .HasAnnotation("Relational:MaxIdentifierLength", 128)
                .HasAnnotation("SqlServer:ValueGenerationStrategy", SqlServerValueGenerationStrategy.IdentityColumn);

            modelBuilder.Entity("GardenHelperWebAPI.Models.Plant", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("int")
                        .HasAnnotation("SqlServer:ValueGenerationStrategy", SqlServerValueGenerationStrategy.IdentityColumn);

                    b.Property<double>("AmountHarvested")
                        .HasColumnType("float");

                    b.Property<string>("CommonName")
                        .HasColumnType("nvarchar(max)");

                    b.Property<string>("DateHarvested")
                        .HasColumnType("nvarchar(max)");

                    b.Property<string>("DatePlanted")
                        .HasColumnType("nvarchar(max)");

                    b.Property<int>("GardenerId")
                        .HasColumnType("int");

                    b.Property<string>("HealthStatus")
                        .HasColumnType("nvarchar(max)");

                    b.Property<double>("Height")
                        .HasColumnType("float");

                    b.Property<string>("ImageUrl")
                        .HasColumnType("nvarchar(max)");

                    b.Property<string>("LastWatering")
                        .HasColumnType("nvarchar(max)");

                    b.Property<double>("Light")
                        .HasColumnType("float");

                    b.Property<double>("SoilMoisture")
                        .HasColumnType("float");

                    b.Property<double>("SoilPH")
                        .HasColumnType("float");

                    b.Property<double>("SpeciesId")
                        .HasColumnType("float");

                    b.HasKey("Id");

                    b.ToTable("Plants");

                    b.HasData(
                        new
                        {
                            Id = 1,
                            AmountHarvested = 0.0,
                            CommonName = "European mountain ash",
                            DateHarvested = "",
                            DatePlanted = "",
                            GardenerId = 1,
                            HealthStatus = "",
                            Height = 0.0,
                            ImageUrl = "https://bs.floristic.org/image/o/63073d2fbf45b90701279405ecc2eec0272906ed",
                            LastWatering = "",
                            Light = 10.0,
                            SoilMoisture = 0.0,
                            SoilPH = 7.0,
                            SpeciesId = 183086.0
                        });
                });
#pragma warning restore 612, 618
        }
    }
}