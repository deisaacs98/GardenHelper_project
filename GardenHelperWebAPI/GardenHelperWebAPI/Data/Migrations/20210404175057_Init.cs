using Microsoft.EntityFrameworkCore.Migrations;

namespace GardenStatsWebAPI.Migrations
{
    public partial class Init : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "EdibleLogs",
                columns: table => new
                {
                    Id = table.Column<int>(nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    PlantId = table.Column<double>(nullable: false),
                    Date = table.Column<string>(nullable: true),
                    Quality = table.Column<int>(nullable: false),
                    Harvested = table.Column<bool>(nullable: false),
                    DaysToHarvest = table.Column<int>(nullable: false),
                    AmountHarvested = table.Column<double>(nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_EdibleLogs", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Logs",
                columns: table => new
                {
                    Id = table.Column<int>(nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    PlantId = table.Column<double>(nullable: false),
                    Date = table.Column<string>(nullable: true),
                    ImageUrl = table.Column<string>(nullable: true),
                    WateredToday = table.Column<bool>(nullable: false),
                    HealthStatus = table.Column<string>(nullable: true),
                    Height = table.Column<double>(nullable: false),
                    SoilPH = table.Column<double>(nullable: false),
                    Light = table.Column<double>(nullable: false),
                    SoilMoisture = table.Column<double>(nullable: false),
                    WaterPrediction = table.Column<bool>(nullable: false),
                    PredictionAccurate = table.Column<bool>(nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Logs", x => x.Id);
                });

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
                    LastWatering = table.Column<string>(nullable: true),
                    HealthStatus = table.Column<string>(nullable: true),
                    Height = table.Column<double>(nullable: false),
                    SoilPH = table.Column<double>(nullable: false),
                    Light = table.Column<double>(nullable: false),
                    SoilMoisture = table.Column<double>(nullable: false),
                    Edible = table.Column<bool>(nullable: false),
                    MinTemp = table.Column<double>(nullable: true),
                    MaxTemp = table.Column<double>(nullable: true),
                    MinPH = table.Column<double>(nullable: true),
                    MaxPH = table.Column<double>(nullable: true),
                    RequiredLight = table.Column<int>(nullable: true),
                    MinPrecipitation = table.Column<double>(nullable: true),
                    MaxPrecipitation = table.Column<double>(nullable: true),
                    SoilHumidity = table.Column<int>(nullable: true),
                    AtmosphericHumidity = table.Column<int>(nullable: true),
                    GardenerId = table.Column<int>(nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Plants", x => x.Id);
                });

            migrationBuilder.InsertData(
                table: "EdibleLogs",
                columns: new[] { "Id", "AmountHarvested", "Date", "DaysToHarvest", "Harvested", "PlantId", "Quality" },
                values: new object[] { 1, 10.0, "", 2, true, 1.0, 0 });

            migrationBuilder.InsertData(
                table: "Logs",
                columns: new[] { "Id", "Date", "HealthStatus", "Height", "ImageUrl", "Light", "PlantId", "PredictionAccurate", "SoilMoisture", "SoilPH", "WaterPrediction", "WateredToday" },
                values: new object[] { 1, "", "", 10.0, "https://bs.floristic.org/image/o/63073d2fbf45b90701279405ecc2eec0272906ed", 10.0, 1.0, true, 0.0, 7.0, true, true });

            migrationBuilder.InsertData(
                table: "Plants",
                columns: new[] { "Id", "AtmosphericHumidity", "CommonName", "DatePlanted", "Edible", "GardenerId", "HealthStatus", "Height", "ImageUrl", "LastWatering", "Light", "MaxPH", "MaxPrecipitation", "MaxTemp", "MinPH", "MinPrecipitation", "MinTemp", "RequiredLight", "SoilHumidity", "SoilMoisture", "SoilPH", "SpeciesId" },
                values: new object[] { 1, 5, "Spinach", "", true, 1, "Good", 10.0, "https://bs.plantnet.org/image/o/3cc08d812a893df9a574b1d377dc5b7c4d6477bc", "", 7.0, 7.5, null, null, 7.0, null, null, 7, null, 0.0, 7.0, 183722.0 });
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "EdibleLogs");

            migrationBuilder.DropTable(
                name: "Logs");

            migrationBuilder.DropTable(
                name: "Plants");
        }
    }
}
