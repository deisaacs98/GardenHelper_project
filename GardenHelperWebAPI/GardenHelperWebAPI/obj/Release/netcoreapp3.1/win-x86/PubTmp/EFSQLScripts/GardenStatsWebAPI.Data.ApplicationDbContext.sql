IF OBJECT_ID(N'[__EFMigrationsHistory]') IS NULL
BEGIN
    CREATE TABLE [__EFMigrationsHistory] (
        [MigrationId] nvarchar(150) NOT NULL,
        [ProductVersion] nvarchar(32) NOT NULL,
        CONSTRAINT [PK___EFMigrationsHistory] PRIMARY KEY ([MigrationId])
    );
END;
GO

BEGIN TRANSACTION;
GO

IF NOT EXISTS(SELECT * FROM [__EFMigrationsHistory] WHERE [MigrationId] = N'20210404175057_Init')
BEGIN
    CREATE TABLE [EdibleLogs] (
        [Id] int NOT NULL IDENTITY,
        [PlantId] float NOT NULL,
        [Date] nvarchar(max) NULL,
        [Quality] int NOT NULL,
        [Harvested] bit NOT NULL,
        [DaysToHarvest] int NOT NULL,
        [AmountHarvested] float NOT NULL,
        CONSTRAINT [PK_EdibleLogs] PRIMARY KEY ([Id])
    );
END;
GO

IF NOT EXISTS(SELECT * FROM [__EFMigrationsHistory] WHERE [MigrationId] = N'20210404175057_Init')
BEGIN
    CREATE TABLE [Logs] (
        [Id] int NOT NULL IDENTITY,
        [PlantId] float NOT NULL,
        [Date] nvarchar(max) NULL,
        [ImageUrl] nvarchar(max) NULL,
        [WateredToday] bit NOT NULL,
        [HealthStatus] nvarchar(max) NULL,
        [Height] float NOT NULL,
        [SoilPH] float NOT NULL,
        [Light] float NOT NULL,
        [SoilMoisture] float NOT NULL,
        [WaterPrediction] bit NOT NULL,
        [PredictionAccurate] bit NOT NULL,
        CONSTRAINT [PK_Logs] PRIMARY KEY ([Id])
    );
END;
GO

IF NOT EXISTS(SELECT * FROM [__EFMigrationsHistory] WHERE [MigrationId] = N'20210404175057_Init')
BEGIN
    CREATE TABLE [Plants] (
        [Id] int NOT NULL IDENTITY,
        [SpeciesId] float NOT NULL,
        [CommonName] nvarchar(max) NULL,
        [ImageUrl] nvarchar(max) NULL,
        [DatePlanted] nvarchar(max) NULL,
        [LastWatering] nvarchar(max) NULL,
        [HealthStatus] nvarchar(max) NULL,
        [Height] float NOT NULL,
        [SoilPH] float NOT NULL,
        [Light] float NOT NULL,
        [SoilMoisture] float NOT NULL,
        [Edible] bit NOT NULL,
        [MinTemp] float NULL,
        [MaxTemp] float NULL,
        [MinPH] float NULL,
        [MaxPH] float NULL,
        [RequiredLight] int NULL,
        [MinPrecipitation] float NULL,
        [MaxPrecipitation] float NULL,
        [SoilHumidity] int NULL,
        [AtmosphericHumidity] int NULL,
        [GardenerId] int NOT NULL,
        CONSTRAINT [PK_Plants] PRIMARY KEY ([Id])
    );
END;
GO

IF NOT EXISTS(SELECT * FROM [__EFMigrationsHistory] WHERE [MigrationId] = N'20210404175057_Init')
BEGIN
    IF EXISTS (SELECT * FROM [sys].[identity_columns] WHERE [name] IN (N'Id', N'AmountHarvested', N'Date', N'DaysToHarvest', N'Harvested', N'PlantId', N'Quality') AND [object_id] = OBJECT_ID(N'[EdibleLogs]'))
        SET IDENTITY_INSERT [EdibleLogs] ON;
    EXEC(N'INSERT INTO [EdibleLogs] ([Id], [AmountHarvested], [Date], [DaysToHarvest], [Harvested], [PlantId], [Quality])
    VALUES (1, 10.0E0, N'''', 2, CAST(1 AS bit), 1.0E0, 0)');
    IF EXISTS (SELECT * FROM [sys].[identity_columns] WHERE [name] IN (N'Id', N'AmountHarvested', N'Date', N'DaysToHarvest', N'Harvested', N'PlantId', N'Quality') AND [object_id] = OBJECT_ID(N'[EdibleLogs]'))
        SET IDENTITY_INSERT [EdibleLogs] OFF;
END;
GO

IF NOT EXISTS(SELECT * FROM [__EFMigrationsHistory] WHERE [MigrationId] = N'20210404175057_Init')
BEGIN
    IF EXISTS (SELECT * FROM [sys].[identity_columns] WHERE [name] IN (N'Id', N'Date', N'HealthStatus', N'Height', N'ImageUrl', N'Light', N'PlantId', N'PredictionAccurate', N'SoilMoisture', N'SoilPH', N'WaterPrediction', N'WateredToday') AND [object_id] = OBJECT_ID(N'[Logs]'))
        SET IDENTITY_INSERT [Logs] ON;
    EXEC(N'INSERT INTO [Logs] ([Id], [Date], [HealthStatus], [Height], [ImageUrl], [Light], [PlantId], [PredictionAccurate], [SoilMoisture], [SoilPH], [WaterPrediction], [WateredToday])
    VALUES (1, N'''', N'''', 10.0E0, N''https://bs.floristic.org/image/o/63073d2fbf45b90701279405ecc2eec0272906ed'', 10.0E0, 1.0E0, CAST(1 AS bit), 0.0E0, 7.0E0, CAST(1 AS bit), CAST(1 AS bit))');
    IF EXISTS (SELECT * FROM [sys].[identity_columns] WHERE [name] IN (N'Id', N'Date', N'HealthStatus', N'Height', N'ImageUrl', N'Light', N'PlantId', N'PredictionAccurate', N'SoilMoisture', N'SoilPH', N'WaterPrediction', N'WateredToday') AND [object_id] = OBJECT_ID(N'[Logs]'))
        SET IDENTITY_INSERT [Logs] OFF;
END;
GO

IF NOT EXISTS(SELECT * FROM [__EFMigrationsHistory] WHERE [MigrationId] = N'20210404175057_Init')
BEGIN
    IF EXISTS (SELECT * FROM [sys].[identity_columns] WHERE [name] IN (N'Id', N'AtmosphericHumidity', N'CommonName', N'DatePlanted', N'Edible', N'GardenerId', N'HealthStatus', N'Height', N'ImageUrl', N'LastWatering', N'Light', N'MaxPH', N'MaxPrecipitation', N'MaxTemp', N'MinPH', N'MinPrecipitation', N'MinTemp', N'RequiredLight', N'SoilHumidity', N'SoilMoisture', N'SoilPH', N'SpeciesId') AND [object_id] = OBJECT_ID(N'[Plants]'))
        SET IDENTITY_INSERT [Plants] ON;
    EXEC(N'INSERT INTO [Plants] ([Id], [AtmosphericHumidity], [CommonName], [DatePlanted], [Edible], [GardenerId], [HealthStatus], [Height], [ImageUrl], [LastWatering], [Light], [MaxPH], [MaxPrecipitation], [MaxTemp], [MinPH], [MinPrecipitation], [MinTemp], [RequiredLight], [SoilHumidity], [SoilMoisture], [SoilPH], [SpeciesId])
    VALUES (1, 5, N''Spinach'', N'''', CAST(1 AS bit), 1, N''Good'', 10.0E0, N''https://bs.plantnet.org/image/o/3cc08d812a893df9a574b1d377dc5b7c4d6477bc'', N'''', 7.0E0, 7.5E0, NULL, NULL, 7.0E0, NULL, NULL, 7, NULL, 0.0E0, 7.0E0, 183722.0E0)');
    IF EXISTS (SELECT * FROM [sys].[identity_columns] WHERE [name] IN (N'Id', N'AtmosphericHumidity', N'CommonName', N'DatePlanted', N'Edible', N'GardenerId', N'HealthStatus', N'Height', N'ImageUrl', N'LastWatering', N'Light', N'MaxPH', N'MaxPrecipitation', N'MaxTemp', N'MinPH', N'MinPrecipitation', N'MinTemp', N'RequiredLight', N'SoilHumidity', N'SoilMoisture', N'SoilPH', N'SpeciesId') AND [object_id] = OBJECT_ID(N'[Plants]'))
        SET IDENTITY_INSERT [Plants] OFF;
END;
GO

IF NOT EXISTS(SELECT * FROM [__EFMigrationsHistory] WHERE [MigrationId] = N'20210404175057_Init')
BEGIN
    INSERT INTO [__EFMigrationsHistory] ([MigrationId], [ProductVersion])
    VALUES (N'20210404175057_Init', N'5.0.5');
END;
GO

COMMIT;
GO

