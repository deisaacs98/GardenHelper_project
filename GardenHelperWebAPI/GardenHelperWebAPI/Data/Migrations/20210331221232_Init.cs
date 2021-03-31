using System;
using Microsoft.EntityFrameworkCore.Migrations;

namespace GardenHelperWebAPI.Migrations
{
    public partial class Init : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Gardeners",
                columns: table => new
                {
                    Id = table.Column<int>(nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    FirstName = table.Column<string>(nullable: true),
                    MiddleInitial = table.Column<string>(nullable: true),
                    LastName = table.Column<string>(nullable: true),
                    Email = table.Column<string>(nullable: true),
                    AddressLine1 = table.Column<string>(nullable: true),
                    AddressLine2 = table.Column<string>(nullable: true),
                    City = table.Column<string>(nullable: true),
                    State = table.Column<string>(nullable: true),
                    Zip = table.Column<int>(nullable: false),
                    Phone = table.Column<int>(nullable: false),
                    Lat = table.Column<double>(nullable: false),
                    Lng = table.Column<double>(nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Gardeners", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Plants",
                columns: table => new
                {
                    Id = table.Column<int>(nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    CommonName = table.Column<string>(nullable: true),
                    DatePlanted = table.Column<DateTime>(nullable: false),
                    DateHarvested = table.Column<DateTime>(nullable: false),
                    LastWatering = table.Column<DateTime>(nullable: false),
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
                table: "Gardeners",
                columns: new[] { "Id", "AddressLine1", "AddressLine2", "City", "Email", "FirstName", "LastName", "Lat", "Lng", "MiddleInitial", "Phone", "State", "Zip" },
                values: new object[] { 1, "", "", "", "", "John", "Gardener", 0.0, 0.0, "J", 0, "", 90210 });

            migrationBuilder.InsertData(
                table: "Plants",
                columns: new[] { "Id", "AmountHarvested", "CommonName", "DateHarvested", "DatePlanted", "GardenerId", "HealthStatus", "Height", "LastWatering", "Light", "SoilMoisture", "SoilPH" },
                values: new object[] { 1, 0.0, "", new DateTime(1, 1, 1, 0, 0, 0, 0, DateTimeKind.Unspecified).AddTicks(1988), new DateTime(1, 1, 1, 0, 0, 0, 0, DateTimeKind.Unspecified).AddTicks(1989), 1, "", 0.0, new DateTime(1, 1, 1, 0, 0, 0, 0, DateTimeKind.Unspecified).AddTicks(1989), 10.0, 0.0, 7.0 });
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Gardeners");

            migrationBuilder.DropTable(
                name: "Plants");
        }
    }
}
