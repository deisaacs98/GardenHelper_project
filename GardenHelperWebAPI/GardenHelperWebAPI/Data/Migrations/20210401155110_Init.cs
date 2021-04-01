﻿using Microsoft.EntityFrameworkCore.Migrations;

namespace GardenHelperWebAPI.Migrations
{
    public partial class Init : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Plants",
                columns: table => new
                {
                    Id = table.Column<int>(nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    SpeciesId = table.Column<double>(nullable: false),
                    CommonName = table.Column<string>(nullable: true),
                    ImageUrl = table.Column<string>(nullable: true),
                    DatePlanted = table.Column<string>(nullable: true),
                    DateHarvested = table.Column<string>(nullable: true),
                    LastWatering = table.Column<string>(nullable: true),
                    HealthStatus = table.Column<string>(nullable: true),
                    Height = table.Column<double>(nullable: false),
                    SoilPH = table.Column<double>(nullable: false),
                    Light = table.Column<double>(nullable: false),
                    SoilMoisture = table.Column<double>(nullable: false),
                    AmountHarvested = table.Column<double>(nullable: false),
                    GardenerId = table.Column<int>(nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Plants", x => x.Id);
                });

            migrationBuilder.InsertData(
                table: "Plants",
                columns: new[] { "Id", "AmountHarvested", "CommonName", "DateHarvested", "DatePlanted", "GardenerId", "HealthStatus", "Height", "ImageUrl", "LastWatering", "Light", "SoilMoisture", "SoilPH", "SpeciesId" },
                values: new object[] { 1, 0.0, "European mountain ash", "", "", 1, "", 0.0, "https://bs.floristic.org/image/o/63073d2fbf45b90701279405ecc2eec0272906ed", "", 10.0, 0.0, 7.0, 183086.0 });
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Plants");
        }
    }
}